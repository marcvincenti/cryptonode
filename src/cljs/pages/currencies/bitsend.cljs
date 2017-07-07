(ns pages.currencies.bitsend
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  (let [mue-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/bitsend/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "BitSend"]
      [coin-infos/masternodes "BitSend"]
      [coin-infos/masternodes-history bitsend-mn-history]]))
