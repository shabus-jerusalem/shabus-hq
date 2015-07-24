angular.module('shabusApp', [])

    .controller('userController', ['$scope', '$http', function($scope, $http) {
        $scope.credentials = "";
        $scope.checked = false;
        $scope.approved = false;
        $scope.text = "No user is approved";

        $scope.validate = function() {
            console.log("hi");
            $http.post('/driver/validate', $scope.credentials)
            .success(function(data, status, headers, config){
                $scope.checked = true;
                $scope.approved = data["approved"];
                $scope.text = data["text"]
            })
            .error(function(data, status, headers, config){
                $scope.checked = false;
                $scope.logout("Not logged In")
            });
        };

    }]);
