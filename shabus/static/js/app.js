angular.module('shabusApp', [])

    .controller('loginController', ['$scope', '$http', function($scope, $http) {
        $scope.user = "";
        $scope.password = "";
        $scope.error_message = null;
        $scope.loggedIn = false

        $scope.login = function(){
            $http.post('/driver/login', [this.user, this.password])
            .success(function(data, status, headers, config){
                $scope.loggedIn = true;
            })
            .error(function(data, status, headers, config){
                console.log($scope.user);
                console.log($scope.password);
            });
        };

        $scope.logout = function(err){
            $scope.error_message = err;
            console.log("Logout1");
            $http.post('/driver/logout')
            .success(function(data, status, headers, config){
                $scope.loggedIn = false;
            })
            .error(function(data, status, headers, config){
                console.log($scope.user);
                console.log($scope.password);
            });
        }
    }])

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