(ns components.menu-bar
  (:require [app.state :refer [app-state]]
            [providers.api :as api]))

(defn component []
  (let [active? (fn [p] (when (= p (:page @app-state)) {:class "active"}))]
    [:nav.navbar.navbar-default
      [:div.container
        [:div.navbar-header
          [:button.navbar-toggle.collapsed {:type "button" :aria-expanded "false"
            :data-toggle "collapse" :data-target "#bs-example-navbar-collapse-1"}
            [:span {:class "icon-bar"}]
            [:span {:class "icon-bar"}]
            [:span {:class "icon-bar"}]]
          [:a {:class "navbar-brand" :href "#/"} "Cryptonode"]]

  [:div.collapse.navbar-collapse {:id "bs-example-navbar-collapse-1"}

    [:ul.nav.navbar-nav
      [:li [:a {:target "_blank" :href "https://docs.google.com/forms/d/e/1FAIpQLSdzlYN3CGdHr-qRdH5IVmbeTFDsRenDQ36EhrSpSXYgRYxsVw/viewform"} "API " [:sub "beta"]]]
      [:li [:a {:target "_blank" :href "https://docs.google.com/forms/d/1_NUGLWjWjujyYGiTylLmlyBa-BSvens6tKCsPSGUxR8/viewform"} "Staking " [:sub "beta"]]]
      ;[:li (active? :about) [:a {:href "#/about"} "About"]]
      ]

      [:form.navbar-form.navbar-right
          [:select.form-control {:value (get-in @app-state [:user-preferences :currency])
            :on-change #(swap! app-state assoc-in [:user-preferences :currency]
                          (-> % .-target .-value))}
            (for [c api/cur-available] ^{:key c} [:option c])]]]]]))
