(ns pages.no-masternodes
  (:require [app.state :refer [app-state]]
            [reagent.core :as r]
            [app.utils :as utils]
            [providers.api :as api]))

(defn form [masternodes-count]
  [:div.row
    [:div.col-md-12
      [:div.input-group
        [:span.input-group-addon "Number of MasterNodes on network"]
        [:input.form-control {:type "number" :value @masternodes-count
          :on-change #(reset! masternodes-count (-> % .-target .-value))}]]]])

(defn table [data masternodes-count]
  (let [user-currency (get-in @app-state [:user-preferences :currency])
        coin-symbol (get data :symbol)
        currency-symbol (api/cur-symbol user-currency)
        price (utils/get-user-price user-currency (get data :price_usd)
                     (get data :price_eur) (get data :price_gbp)
                     (get data :price_btc))
        blocks-per-day (get data :blocks_per_day)
        masternodes-reward (get data :masternodes_reward)
        masternodes-cost (get data :masternodes_cost)
        masternodes-monthly-revenue (/ (* masternodes-reward blocks-per-day 30.42) @masternodes-count)
        masternodes-waiting-time (/ @masternodes-count blocks-per-day)]
    [:table.table [:tbody
      [:tr [:th.col-sm-6 "Actual Coin Supply"]
        [:td (-> (get data :available_supply)
                 (Math/round)
                 (str)
                 (utils/kilo-numbers)) " " coin-symbol]]
        [:tr [:th "Masternode Cost"]
          [:td (-> masternodes-cost
                  (Math/round)
                  (str)
                  (utils/kilo-numbers)) " " coin-symbol " = "
                  (utils/format-number (* masternodes-cost price)) currency-symbol]]
        [:tr [:th "Masternode Rewards"]
          [:td (-> masternodes-reward
                   (utils/format-number)) " " coin-symbol " = "
                   (utils/format-number (* masternodes-reward price)) currency-symbol
                   " (every " (if (> masternodes-waiting-time 2)
                    (str (utils/format-number masternodes-waiting-time) " days)")
                    (str (utils/format-number (* 24 masternodes-waiting-time)) " hours)"))]]
        [:tr [:th "Monthly Income"]
          [:td (-> masternodes-monthly-revenue
                   (utils/format-number)) " " coin-symbol " = "
                   (utils/format-number (* masternodes-monthly-revenue price)) currency-symbol]]
        [:tr [:th "Calculated ROI (monthly)"]
          [:td (-> (/ (* masternodes-monthly-revenue 100) masternodes-cost)
                    (utils/format-number)) "%"]]
        ]]))

(defn component [coin-name]
  (let [mn-number (r/atom 1000)]
    [:div {:class "container"}
      [:h1 {:class "page-header"} coin-name]
      [form mn-number]
      [:br]
      [:div.panel.panel-default
        [:div.panel-heading coin-name " Masternodes"]
          [table (api/get-currency coin-name) mn-number]]]))
