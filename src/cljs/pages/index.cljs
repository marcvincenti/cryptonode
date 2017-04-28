(ns pages.index
  (:require [app.state :refer [app-state]]
            [clojure.string :as string]
            [reagent.core :as r]
            [app.utils :as utils]
            [providers.api :as api]))

(defn update-sort-value [new-val]
  (if (= new-val (get-in @app-state [:user-preferences :sort-val]))
    (swap! app-state update-in [:user-preferences :ascending] not)
    (swap! app-state assoc-in [:user-preferences :ascending] (= new-val :coin)))
  (swap! app-state assoc-in [:user-preferences :sort-val] new-val))

(defn sorted-contents []
  (let [table-contents (get @app-state :api-data)
        column (get-in @app-state [:user-preferences :sort-val])
        sorted-contents (->> table-contents (sort-by (cond
        (= column :market-cap) #(* (get % :available_supply) (get % :price_btc))
        (= column :masternode-cost) #(* (get % :masternodes_cost) (get % :price_btc))
        (= column :monthly-revenue) #(* (get % :masternodes_monthly_revenue) (get % :price_btc))
        (= column :roi) #(/ (get % :masternodes_monthly_revenue) (get % :masternodes_cost))
        :else column)))]
    (if (get-in @app-state [:user-preferences :ascending])
      sorted-contents
      (rseq sorted-contents))))

(defn table []
  (let [user-currency (get-in @app-state [:user-preferences :currency])
        currency-symbol (api/cur-symbol user-currency)]
  [:table.table.table-hover
   [:thead
    [:tr
     [:th {:on-click #(update-sort-value :coin)} "Name"]
     [:th {:on-click #(update-sort-value :market-cap)} "Market Cap"]
     [:th {:on-click #(update-sort-value :masternode-cost)} "Masternode Cost"]
     [:th {:on-click #(update-sort-value :monthly-revenue)} "Monthly Revenue"]
     [:th {:on-click #(update-sort-value :roi)} "R.O.I"]]]
    [:tbody
     (for [{:keys [coin
                   available_supply
                   masternodes_cost
                   masternodes_monthly_revenue
                   price_usd
                   price_btc
                   price_eur]} (sorted-contents)
          :let [price (utils/get-user-price user-currency price_usd price_eur price_btc)]] ^{:key coin}
       [:tr
         [:td [:a {:href (str "#/currency/" (string/lower-case coin))} coin]]
         [:td (utils/kilo-numbers (str (int (* available_supply price)))) currency-symbol]
         [:td (utils/format-number (* masternodes_cost price)) currency-symbol]
         [:td (utils/format-number (* masternodes_monthly_revenue price)) currency-symbol]
         [:td (utils/format-number (* 100 (/ masternodes_monthly_revenue masternodes_cost)))"%"]])]]))

(defn component []
  [:div.container
    [:h1.page-header "CryptoCurrency Masternode Earnings"]
    (when (get @app-state :api-data) [table])])
