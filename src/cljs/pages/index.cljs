(ns pages.index
  (:require [app.state :refer [app-state]]
            [clojure.string :as string]
            [reagent.core :as r]
            [app.utils :as utils]
            [providers.api :as api]))

(defn filter-content
  [filterstring]
  (filter #(re-find (->> (str filterstring)
                         (string/upper-case)
                         (re-pattern))
                    (string/upper-case (:coin %)))
          (get @app-state :api-data)))

(defn table
  [myfilter]
  (let [currency-symbol (api/cur-symbol (get @app-state :user-currency))]
  [:table {:class "table table-condensed"}
   [:thead
    [:tr
     [:th "Name"]
     [:th "Market Cap"]
     [:th "Masternode Cost"]
     [:th "Monthly Revenue"]
     [:th "R.O.I"]]]
    [:tbody
     (for [{:keys [coin
                   available_supply
                   masternodes_cost
                   masternodes_monthly_revenue
                   price_usd]} (filter-content myfilter)] ^{:key coin}
       [:tr
         [:td coin]
         [:td (utils/format-number (* available_supply price_usd)) currency-symbol]
         [:td (utils/format-number (* masternodes_cost price_usd)) currency-symbol]
         [:td (utils/format-number (* masternodes_monthly_revenue price_usd)) currency-symbol]
         [:td (utils/format-number (* 100 (/ masternodes_monthly_revenue masternodes_cost)))"%"]])]]))

(defn navbar-table
  [myFilter]
  [:nav.navbar.navbar-default
    [:form.navbar-form.navbar-left
      [:select.form-control {:value (get @app-state :user-currency)
        :on-change #(swap! app-state assoc :user-currency
                      (-> % .-target .-value))}
        (for [c api/cur-available] ^{:key c} [:option c])]]
    [:div.input-group.stylish-input-group
      [:form.navbar-form
        [:input.form-control {:type "text" :value @myFilter
                :placeholder "Search"
                :on-change #(reset! myFilter (-> % .-target .-value))}]
        [:span.input-group-addon
          [:button {:type "submit"} [:span.glyphicon.glyphicon-search]]]]]])

(defn search-table
  []
  (let [filter-value (r/atom nil)]
    (fn []
      [:div
        [navbar-table filter-value]
        (when (get @app-state :api-data) [table @filter-value])])))

(defn component []
  [:div.container
    [:h1.page-header "CryptoCurrency Masternode Earnings"]
    [search-table]])
