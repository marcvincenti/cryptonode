(ns pages.currencies.crown
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  (let [crown-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/crown/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "Crown"]
      [coin-infos/masternodes "Crown"]
      [coin-infos/masternodes-history crown-mn-history]]))
