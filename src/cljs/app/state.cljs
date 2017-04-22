(ns app.state
  (:require [reagent.core :as r]))

(defonce app-state (r/atom {
  :user-currency "USD"
  }))
