(ns providers.api
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [app.state :refer [app-state]]))

(def cur-available ["BTC", "EUR", "USD"])
(def ^:private url "")

(defn update-data
  "Load masternodes data from the api"
  []
  (go (let [response (<! (http/get url {:with-credentials? false}))]
    (when (:success response)
      (.log js/console (str response))))))
