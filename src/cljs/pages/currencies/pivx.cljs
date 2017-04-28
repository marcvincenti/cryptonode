(ns pages.currencies.pivx
  (:require [app.state :refer [app-state]]
            [app.utils :as utils]
            [components.coin-infos :as coin-infos]
            [providers.api :as api]))

(def ^:private blocks-per-day 1440)
(def ^:private blocks-per-month (* 30.4167 blocks-per-day))

(defn compare-with-st []
  (let [data (api/get-currency "PIVX")
        user-currency (get-in @app-state [:user-preferences :currency])
        currency-symbol (api/cur-symbol user-currency)
        price (utils/get-user-price user-currency (get data :price_usd)
                           (get data :price_eur) (get data :price_btc))
        mn-count (get data :masternodes_count)
        supply (get data :available_supply)
        mn-cost (get data :masternodes_cost)
        mn-reward (get data :masternodes_reward)
        st-reward (- 9 mn-reward)
        mn-monthly-revenue (get data :masternodes_monthly_revenue)
        waiting-time-masternode (get data :masternodes_reward_waiting_time)
        total-staking (* (- supply (* mn-cost mn-count)) 0.65)
        waiting-time-staking (/ total-staking (* blocks-per-day 10000))
        st-monthly-revenue (/ (* 10000 blocks-per-month st-reward) total-staking)]
    [:div {:class "panel panel-default"}
      [:div {:class "panel-heading"} "Masternodes VS Staking"]
      [:table {:class "table"} [:tbody
        [:tr [:th {:class "col-sm-2"} "#"]
             [:th {:class "col-sm-5"} "Masternodes"]
             [:th {:class "col-sm-5"} "Staking"]]
        [:tr [:th "Requirements"]
          [:td (str mn-cost " PIVX ")
            [:sub (utils/format-number (* mn-cost price)) currency-symbol]]
          [:td "> 1 PIVX"]]
        [:tr [:th "Reward"]
          [:td (utils/format-number mn-reward) " PIVX "
            [:sub (utils/format-number (* mn-reward price)) currency-symbol]]
          [:td (utils/format-number st-reward) " PIVX "
            [:sub (utils/format-number (* st-reward price)) currency-symbol]]]
        [:tr [:th "Average waiting time"]
          [:td (utils/format-number waiting-time-masternode) " days"]
          [:td (utils/format-number waiting-time-staking) " days"]]
        [:tr [:th "Monthly revenue"]
          [:td (utils/format-number mn-monthly-revenue) " PIVX "
            [:sub (utils/format-number (* mn-monthly-revenue price)) currency-symbol]]
          [:td (utils/format-number st-monthly-revenue) " PIVX "
            [:sub (utils/format-number (* st-monthly-revenue price)) currency-symbol]]]]]]))

(defn component []
  [:div {:class "container"}
    [:h1 {:class "page-header"} "PIVX"]
    [coin-infos/masternodes "PIVX"]
    [compare-with-st]])
