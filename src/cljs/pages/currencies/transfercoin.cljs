(ns pages.currencies.transfercoin
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  [:div {:class "container"}
    [:h1 {:class "page-header"} "TransferCoin"]
    [coin-infos/masternodes "TransferCoin"]])
