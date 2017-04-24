(ns components.footer
  (:require [app.state :refer [app-state]]))

(defn component []
  [:footer.footer
    [:div.navbar.navbar-default.navbar-fixed-bottom
      [:div.container
        [:p.navbar-text.pull-left "Contact : "
             [:a {:href "mailto:hello@cryptonode.co" :target "_blank"}
                  "hello@cryptonode.co"]]]]])
