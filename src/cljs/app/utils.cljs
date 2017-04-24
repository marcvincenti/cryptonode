(ns app.utils
  (:require [cljs.pprint :as pprint]
            [app.state :refer [app-state]]))

(defn kilo-numbers
  "Add a comma every power of 1k"
  [number]
  (clojure.string/replace
    number
    #"\B(?=(\d{3})+(?!\d))" ","))

(defn format-number
  "Format a float number"
  [number]
  (kilo-numbers
    (pprint/cl-format nil "~,2f" number)))

(defn get-user-price
  "Take all currencies but only return the price the user have choosen"
  [c usd eur btc]
  (case c
        "USD" usd
        "EUR" eur
        "BTC" btc
        "" 0))
