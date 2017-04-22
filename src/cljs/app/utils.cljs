(ns app.utils
  (:require [cljs.pprint :as pprint]))

(defn format-number
  "Format a float number"
  [number]
  (pprint/cl-format nil "~,2f" number))
