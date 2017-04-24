(ns components.menu-bar
  (:require [app.state :refer [app-state]]))

(defn component []
  (let [active? (fn [p] (when (= p (:page @app-state)) {:class "active"}))]
    [:nav.navbar.navbar-default
      [:div.container
        [:div.navbar-header
          [:button.navbar-toggle.collapsed {:type "button" :aria-expanded "false"}
            [:span {:class "icon-bar"}]
            [:span {:class "icon-bar"}]
            [:span {:class "icon-bar"}]]
          [:a {:class "navbar-brand" :href "#/"} "Cryptonode"]]

  [:div.collapse.navbar-collapse

    [:ul.nav.navbar-nav
      [:li [:a {:target "_blank" :href "https://docs.google.com/forms/d/e/1FAIpQLSdzlYN3CGdHr-qRdH5IVmbeTFDsRenDQ36EhrSpSXYgRYxsVw/viewform"} "API " [:sub "beta"]]]
      [:li [:a {:target "_blank" :href "https://docs.google.com/forms/d/1_NUGLWjWjujyYGiTylLmlyBa-BSvens6tKCsPSGUxR8/viewform"} "Staking " [:sub "beta"]]]
      [:li (active? :about) [:a {:href "#/about"} "About"]]]]]]))
