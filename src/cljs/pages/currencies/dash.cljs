(ns pages.currencies.dash
  (:require [app.state :refer [app-state]]
            [components.coin-infos :as coin-infos]))

(defn component []
  (let [dash-mn-history "https://318h5of2kh.execute-api.eu-west-1.amazonaws.com/dev/currency/dash/history"]
    [:div {:class "container"}
      [:h1 {:class "page-header"} "Dash"]
      [coin-infos/masternodes "Dash"]
      [coin-infos/masternodes-history dash-mn-history]]))
