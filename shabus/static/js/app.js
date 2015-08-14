angular.module('shabusApp', [])

    .controller('userController', ['$scope', '$sce', '$http', '$interval', '$window',
                function($scope, $sce, $http, $interval, $window) {
        $scope.credentials = "";
        $scope.checked = false;
        $scope.approved = false;
        $scope.text = "";
        $scope.counter = 0;
        $scope.hasPosition = false;
        $scope.waiting = false;

        var position = {
            "accuracy" : null,
            "latitude" : null,
            "longitude" : null,
            "speed" : null
        };
        var interval = null;
        var retry = 5;


        $window.navigator.geolocation.watchPosition(function(current_position){
            $scope.$apply(function(){
                $scope.hasPosition = true;
            });
            position = {
                    "accuracy" : current_position["coords"].accuracy,
                    "latitude" : current_position["coords"].latitude,
                    "longitude" : current_position["coords"].longitude,
                    "speed" : current_position["coords"].speed
                };
        }, function(err){
            $scope.$apply(function(){
                $scope.hasPosition = false;
            });
            position = {
                "accuracy" : null,
                "latitude" : null,
                "longitude" : null,
                "speed" : null
            };
        },
        { "maximumAge" : 30000, "timeout" : 1000 });

        $scope.showResult = function(approved, text){
            $scope.credentials = "";
            $scope.counter = 5;
            interval = $interval($scope.countdown, 1000);

            $scope.checked = true;
            $scope.approved = approved;
            $scope.text = $sce.trustAsHtml(text);
            if (approved){
                document.getElementById('success').play()
            } else {
                document.getElementById('fail').play()
            }
        }

        $scope.approve = function() {
            $scope.waiting = true;
            console.log(position);
            $http.post('/driver/approve', {"id" : $scope.credentials, "position" : position})
            .success(function(data, status, headers, config){
                $scope.waiting = false;
                $scope.showResult(data["status"] == "OK", data["data"]["text"]);
            })
            .error(function(data, status, headers, config){
                $scope.waiting = false;
                // Logout in case user isn't logged in
                if (status >= 400 && status < 500){
                    $scope.credentials = "";
                    $window.location.href = '/login';
                }
                // In case of other error:
                else {
                    retry--;
                    if (retry > 0){
                        $scope.approve();
                    } else {
                        $scope.showResult(false, "מצטערים, ארעה שגיאה באימות. אנא נסו שנית.");
                        retry = 5;
                    }
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

        $scope.reset = function(){
            $scope.checked = false;
            $scope.counter=0;
            $interval.cancel(interval);
        }

    }]);
