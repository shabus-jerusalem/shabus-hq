angular.module('shabusApp', [])

    .controller('userController', ['$scope', '$http', '$interval', '$window',
                function($scope, $http, $interval, $window) {
        $scope.credentials = "";
        $scope.checked = false;
        $scope.approved = false;
        $scope.text = "";
        $scope.counter = 0;
        $scope.hasPosition = false;

        var position = {
            "accuracy" : null,
            "latitude" : null,
            "longitude" : null,
            "speed" : null
        };
        var interval = null;


        $window.navigator.geolocation.watchPosition(function(current_position){
            $scope.hasPosition = true;
            position = {
                    "accuracy" : current_position["coords"].accuracy,
                    "latitude" : current_position["coords"].latitude,
                    "longitude" : current_position["coords"].longitude,
                    "speed" : current_position["coords"].speed
                };
        }, function(err){
            $scope.hasPosition = false;
            position = {
                "accuracy" : null,
                "latitude" : null,
                "longitude" : null,
                "speed" : null
            };
        },
        { "maximumAge" : 30000, "timeout" : 1000 });

        $scope.approve = function() {
            console.log(position);
            $http.post('/driver/approve', {"id" : $scope.credentials, "position" : position})
            .success(function(data, status, headers, config){
                $scope.counter = 5;
                interval = $interval($scope.countdown, 1000);

                $scope.checked = true;
                $scope.approved = data["status"] == "OK";
                $scope.text = data["data"]["text"]            
            })
            .error(function(data, status, headers, config){
                // Logout in case user isn't logged in
                if (status >= 400 && status < 500){
                    $window.location.href = '/login';
                }
            });
        };


        $scope.countdown = function(){
            $scope.counter--;
            if ($scope.counter <= 0){
                $scope.checked = false;
                $interval.cancel(interval);
            }
        }

    }]);
