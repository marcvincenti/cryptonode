(ns pages.currencies.pivx
  (:require [reagent.core :as r]
            [app.state :refer [app-state]]
            [app.utils :as utils]
            [components.coin-infos :as coin-infos]
            [providers.api :as api]))

(def ^:private blocks-per-day 1440)
(def ^:private blocks-per-month (* 30.4167 blocks-per-day))

(defn staking [nb-pivx]
  (let [data (api/get-currency "PIVX")
        user-currency (get-in @app-state [:user-preferences :currency])
        currency-symbol (api/cur-symbol user-currency)
        price (utils/get-user-price user-currency (get data :price_usd)
                           (get data :price_eur) (get data :price_gbp)
                           (get data :price_btc))
        mn-count (get data :masternodes_count)
        supply (get data :available_supply)
        mn-cost (get data :masternodes_cost)
        mn-reward (get data :masternodes_reward)
        st-reward (- 4.5 mn-reward)
        total-staking (* (- supply (* mn-cost mn-count)) 0.65)
        staking-waiting-time (/ total-staking (* blocks-per-day @nb-pivx))
        staking-monthly-revenue (/ (* @nb-pivx blocks-per-month st-reward) total-staking)]
    [:div.panel.panel-default
      [:div.panel-heading
        [:div.input-group.col-sm-4
          [:span.input-group-addon "Staking"]
          [:input.form-control {:type "number" :value @nb-pivx
              :on-change #(reset! nb-pivx (-> % .-target .-value))}]]]
      [:table.table [:tbody
        [:tr [:th.col-sm-6 "Staked PIVX"]
          [:td (-> @nb-pivx
                   (Math/round)
                   (str)
                   (utils/kilo-numbers)) " PIVX "
            [:sub (utils/format-number (* @nb-pivx price)) currency-symbol]]]
        [:tr [:th "Staking Rewards"]
          [:td (-> st-reward
                   (utils/format-number)) " PIVX "
            [:sub (utils/format-number (* st-reward price)) currency-symbol]
            " / " (if (> staking-waiting-time 2)
                    (str (utils/format-number staking-waiting-time) " days")
                    (str (utils/format-number (* 24 staking-waiting-time)) " hours"))]]
        [:tr [:th "Monthly Income"]
          [:td (-> staking-monthly-revenue
                   (utils/format-number)) " PIVX "
            [:sub (utils/format-number (* staking-monthly-revenue price)) currency-symbol]]]
            ]]]))

(defn component []
  (let [staking-pivx (r/atom 10000)
        pivx-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/pivx/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "PIVX"]
      [coin-infos/masternodes "PIVX"]
      [staking staking-pivx]
      [coin-infos/masternodes-history pivx-mn-history]]))
