(function () {
    function updateStorage(storageKey, extraValue) {
        let current = sessionStorage.getItem(storageKey);
        let storageValue = [];
        if (current !== null) {
            storageValue = JSON.parse(current);
        }
        storageValue.push(extraValue);
        sessionStorage.setItem(storageKey, JSON.stringify(storageValue));
    }

    /////////////////////////////////////
    // grantPermissions fails to change Notification.permission in headless Chrome?? https://github.com/puppeteer/puppeteer/issues/3279
    /////////////////////////////////////

    /*
    // hardcoded on load to avoid delays waiting for Notification.requestPermission promise to resolve
    // TODO causes notification request popup
    Notification.requestPermission().then(function(result) {
        Object.defineProperty(Notification, "permission", {
                get() {
                    updateStorage('__DetectNotificationPermissionRequestNotificationPermission', {"href": window.location.href,
                            "value": "default", "hardcoded": true});
                    return "default";
                }
            }
        )
        ////console.log("P>",Notification.permission);
    });

    // console.log("A>", "safari" in window && "pushNotification" in window.safari ? window.safari.pushNotification.permission(_at.webpushid).permission : "Notification" in window && "permission" in window.Notification ? Notification.permission : void 0);
    // console.log("B>", "Notification" in window)
    // console.log("C>", "permission" in window.Notification )
   //// console.log("D>",Notification.permission)
    ////Notification.requestPermission().then(result => console.log("E>",result));
   //// navigator.permissions.query({name:'notifications'}).then(function(permissionStatus) {
   ////     console.log("G>", permissionStatus.state)
   //// });

    // grantPermissions fails to change Notification.permission in headless Chrome?? https://github.com/puppeteer/puppeteer/issues/3279

    Notification.requestPermission().then(function(result) {
    // TODO causes notification request popup
     // ALT: navigator.permissions.query('notifications').then(function (result) {
       Object.defineProperty(Notification, "permission", {
                get() {
                        updateStorage('__DetectNotificationPermissionRequestNotificationPermission', {"href": window.location.href,
                            "value": result, //ALT result.state, // result,
                            "hardcoded": false});
                    return result; //ALT result.state;
                }
            }
        );
       ////console.log("L>",Notification.permission);
    });
       //// console.log("H>",Notification.permission);
    ////Notification.requestPermission().then(result => console.log("I>",result));
  ////  navigator.permissions.query({name:'notifications'}).then(function(permissionStatus) {
  ////      console.log("J>", permissionStatus.state)
  ////  });
    ////    console.log("K>",Notification.permission);
   */

    let orig_permission = Notification.permission;
    Object.defineProperty(Notification, "permission", {
        get() {
            updateStorage('__DetectNotificationPermissionRequestNotificationPermission', {"href": window.location.href,
                    "value": orig_permission,
                    "hardcoded": false});
            return orig_permission;
        }
    });


    let orig_requestPermission = Notification.requestPermission;
    Notification.requestPermission = function () {
        let returned_promise = orig_requestPermission.apply(this, arguments);
        updateStorage('__DetectNotificationPermissionRequestNotificationRequestPermission', {"href": window.location.href});
        return returned_promise;
    };
    ////Notification.requestPermission().then(result => console.log("F>",result));

    let orig_Subscribe = PushManager.prototype.subscribe;
    PushManager.prototype.subscribe = function () {
        let logValue = {"href": window.location.href, "arguments": arguments[0]};
        let returned_promise = orig_Subscribe.apply(this, arguments);
        returned_promise.then(function (pushSubscription) {
                logValue["pushSubscription"] = pushSubscription
            },
            function (err) {
                logValue["error"] = err
            });
        updateStorage('__DetectNotificationPermissionRequestPushSubscribe', logValue);
        return returned_promise;
    };

    let orig_permissionState = PushManager.prototype.permissionState;
    PushManager.prototype.permissionState = function () {
        let logValue = {"href": window.location.href, "arguments": arguments[0]};
        let returned_promise = orig_permissionState.apply(this, arguments);
        returned_promise.then(function (pushMessagingState) {
                logValue["pushMessagingState"] = pushMessagingState
            },
            function (err) {
                logValue["error"] = err
            });
        updateStorage('__DetectNotificationPermissionRequestPushPermissionState', logValue);
        return returned_promise;
    };


    let orig_getSubscription = PushManager.prototype.getSubscription;
    PushManager.prototype.getSubscription = function () {
        let logValue = {"href": window.location.href, "arguments": arguments[0]};
        let returned_promise = orig_getSubscription.apply(this, arguments);
        returned_promise.then(function (pushSubscription) {
                logValue["pushSubscription"] = pushSubscription
            },
            function (err) {
                logValue["error"] = err
            });
        updateStorage("__DetectNotificationPermissionRequestPushGetSubscription", logValue);
        return returned_promise;

    };

    let orig_permissionsQuery = navigator.permissions.query;
    navigator.permissions.query = function () {  // TODO note that this can also be used to detect other permission requests, e.g. geolocation
        let queryType = arguments[0].name;
        if (queryType === "push" || queryType === "notifications") {
            let logValue = {"href": window.location.href, "arguments": arguments[0], "queryType": queryType};
            updateStorage('__DetectNotificationPermissionRequestPermissionsQuery', logValue);
        }
        return orig_permissionsQuery.apply(this, arguments);
    }
})();