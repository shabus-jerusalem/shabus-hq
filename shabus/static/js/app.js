angular.module('shabusApp', [])

    .controller('userController', ['$scope', '$http', '$interval', '$window',
                function($scope, $http, $interval, $window) {
        $scope.credentials = "";
        $scope.checked = false;
        $scope.approved = false;
        $scope.text = "";
        $scope.counter = 0

        var interval = null;

        $scope.validate = function() {
            console.log("hi");
            $http.post('/driver/approve', $scope.credentials)
            .success(function(data, status, headers, config){
                console.log(data)
                $scope.counter = 5;
                interval = $interval($scope.countdown, 1000);
                $scope.checked = true;
                $scope.approved = data["status"] == "OK";
                $scope.text = data["data"]["text"]            
            })
            .error(function(data, status, headers, config){
                // Logout in case user isn't logged in
                $window.location.href = '/login';
            });
        };


        $scope.countdown = function(){
            $scope.counter--;
            if ($scope.counter <= 0){
                $scope.checked = false;
                $interval.cancel(interval)
            }
        }

    }]);
