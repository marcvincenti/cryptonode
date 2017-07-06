(ns pages.currencies.mue
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  (let [mue-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/mue/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "MonetaryUnit"]
      [coin-infos/masternodes "MonetaryUnit"]
      [coin-infos/masternodes-history mue-mn-history]]))
