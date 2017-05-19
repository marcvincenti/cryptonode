(ns pages.currencies.transfercoin
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  (let [tx-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/tx/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "TransferCoin"]
      [coin-infos/masternodes "TransferCoin"]
      [coin-infos/masternodes-history tx-mn-history]]))
