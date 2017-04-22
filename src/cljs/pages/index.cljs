(ns pages.index
  (:require [app.state :refer [app-state]]
            [clojure.string :as string]
            [reagent.core :as r]
            [providers.calculator :as calc]))

(defn filter-content
  [filterstring]
  (filter #(re-find (->> (str filterstring)
                         (string/upper-case)
                         (re-pattern))
                    (string/upper-case (:coin %)))
          (get @app-state :api-data)))

(defn table
  [myfilter]
  [:table {:class "table table-condensed"}
   [:thead
    [:tr
     [:th "Name"]
     [:th "Supply"]
     [:th "Price"]]]
    [:tbody
     (for [{:keys [coin
                   available_supply
                   price_usd]} (filter-content myfilter)]
       ^{:key coin}
       [:tr
         [:td coin]
         [:td available_supply]
         [:td price_usd]])]])

(defn search-table
  []
  (let [filter-value (r/atom nil)]
    (fn []
      [:div
       [:input {:type "text" :value @filter-value
                :on-change #(reset! filter-value (-> % .-target .-value))}]
       [table @filter-value]])))

(defn component []
  [:div.container
    [:h1.page-header "CryptoCurrency Masternode Earnings"]
    (when (get @app-state :api-data) [search-table])])
