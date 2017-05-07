(ns components.coin-infos
  (:require [app.state :refer [app-state]]
            [app.utils :as utils]
            [providers.api :as api]))

(defn masternodes [coin]
  (let [data (api/get-currency coin)
        user-currency (get-in @app-state [:user-preferences :currency])
        coin-symbol (get data :symbol)
        currency-symbol (api/cur-symbol user-currency)
        price (utils/get-user-price user-currency (get data :price_usd)
                     (get data :price_eur) (get data :price_btc))
        masternodes-reward (get data :masternodes_reward)
        masternodes-cost (get data :masternodes_cost)
        masternodes-monthly-revenue (get data :masternodes_monthly_revenue)
        masternodes-waiting-time (get data :masternodes_reward_waiting_time)]
  [:div.panel.panel-default
    [:div.panel-heading coin " Masternodes"]
    [:table.table [:tbody
      [:tr [:th.col-sm-6 "Actual Coin Supply"]
        [:td (-> (get data :available_supply)
                 (int)
                 (str)
                 (utils/kilo-numbers)) " " coin-symbol]]
        [:tr [:th "Number of Masternodes"]
          [:td (-> (get data :masternodes_count)
                  (str)
                  (utils/kilo-numbers))]]
        [:tr [:th "Masternode Cost"]
          [:td (-> masternodes-cost
                  (int)
                  (str)
                  (utils/kilo-numbers)) " " coin-symbol " "
            [:sub (utils/format-number (* masternodes-cost price)) currency-symbol]]]
        [:tr [:th "Masternode Rewards"]
          [:td (-> masternodes-reward
                   (utils/format-number)) " " coin-symbol " "
            [:sub (utils/format-number (* masternodes-reward price)) currency-symbol]
            " / " (if (> masternodes-waiting-time 2)
                    (str (utils/format-number masternodes-waiting-time) " days")
                    (str (utils/format-number (* 24 masternodes-waiting-time)) " hours"))]]
        [:tr [:th "Monthly Income"]
          [:td (-> masternodes-monthly-revenue
                   (utils/format-number)) " " coin-symbol " "
            [:sub (utils/format-number (* masternodes-monthly-revenue price)) currency-symbol]]]
        ]]]))
