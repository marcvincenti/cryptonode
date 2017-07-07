(ns app.core
  (:require-macros [secretary.core :refer [defroute]])
  (:import goog.History)
  (:require [secretary.core :as secretary]
            [goog.events :as events]
            [goog.history.EventType :as EventType]
            [reagent.core :as r]
            [app.state :refer [app-state]]
            [components.menu-bar :as menu-bar]
            [components.footer :as footer]
            [providers.api :as api]
            [pages.index :as index]
            [pages.currencies.bitsend :as bitsend-page]
            [pages.currencies.dash :as dash-page]
            [pages.currencies.crown :as crown-page]
            [pages.currencies.mue :as mue-page]
            [pages.currencies.pivx :as pivx-page]
            [pages.currencies.transfercoin :as transfercoin-page]))

;access to google analytics
(defn ga [& more]
  (when js/ga
    (.. (aget js/window "ga")
        (apply nil (clj->js more)))))

;Adding Browser History
(defn hook-browser-navigation! []
  (doto (History.)
    (events/listen
     EventType/NAVIGATE
     (fn [event]
       (do
         (secretary/dispatch! (.-token event))
         ;google analytics
         (ga "set" "page" (str (get @app-state :page)))
         (ga "send" "pageview"))))
    (.setEnabled true)))

;Page routes definition
(defn app-routes []
  (secretary/set-config! :prefix "#")
  (defroute "/" [] (swap! app-state assoc :page :index))
  (defroute "/currency/bitsend" [] (swap! app-state assoc :page :bitsend-page))
  (defroute "/currency/crown" [] (swap! app-state assoc :page :crown-page))
  (defroute "/currency/dash" [] (swap! app-state assoc :page :dash-page))
  (defroute "/currency/monetaryunit" [] (swap! app-state assoc :page :mue-page))
  (defroute "/currency/pivx" [] (swap! app-state assoc :page :pivx-page))
  (defroute "/currency/transfercoin" [] (swap! app-state assoc :page :transfercoin-page))
  (hook-browser-navigation!))

;Current-page multimethod : return which page to display based on app-state
(defmulti current-page #(@app-state :page))
(defmethod current-page :index [] [index/component])
(defmethod current-page :bitsend-page [] [bitsend-page/component])
(defmethod current-page :crown-page [] [crown-page/component])
(defmethod current-page :dash-page [] [dash-page/component])
(defmethod current-page :mue-page [] [mue-page/component])
(defmethod current-page :pivx-page [] [pivx-page/component])
(defmethod current-page :transfercoin-page [] [transfercoin-page/component])
(defmethod current-page :default  [] [:div])

;Root function to run cljs app
(defn ^:export run []
  (app-routes)
  (api/update-data)
  (r/render [menu-bar/component] (.getElementById js/document "menu-bar"))
  (r/render [footer/component] (.getElementById js/document "footer-bar"))
  (r/render [current-page]
    (.getElementById js/document "app-container")))
