(ns pages.index
  (:require [app.state :refer [app-state]]
            [providers.calculator :as calc]))

(defn component []
  [:div {:class "container"}
    [:h1 {:class "page-header"} "Cryptocurrencies with Masternodes systems"]
    [:div {:class "col-sm-12"}
      "Hello world !"]])
