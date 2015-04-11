define('homeController', ['app', 'Uploader', 'UploadVideoCover', 'factories', 'less!homeStyle', 'css!ngDropdownStyle'], function(app, Upload, UploadVideoCover){

  app


    .controller('home', function($scope, $http){
      $scope.tab = [];
      for (var i = 0; i < 6; ++i)
        $scope.tab[i] = {};
      $scope.changeTab = function(tabIndex){
        for (var i = 0; i < 6; ++i)
          $scope.tab[i].isActive = false;
        $scope.tab[tabIndex].isActive = true;
      }
      $scope.changeTab(4);

    })


  .controller('tab2', function($scope, $http){
  })


  .controller('tab4', ['$scope', '$http', 'collectionUrl', function($scope, $http, collectionUrl){

    $scope.allvideofiles = [];
    $scope.changeVideoFiles = function() {
      console.log($scope.videofiles);
      for (var i=0; i<$scope.videofiles.length; i++) {
        $scope.allvideofiles.push($scope.videofiles[i]);
      }
      console.log($scope.allvideofiles);
    };

    //collections Selected
    $scope.collection = {};
    $scope.collection.options = [];
    $scope.collection.selected = {
      'name': '请选择'
    };
    $http.get(collectionUrl + 'is_member_of')
      .success(function(res){
        $scope.collection.options = res;
      });

    $scope.videoCover = [];
    uploadVideoCover = new UploadVideoCover(document.getElementById('video-cover'), document.getElementById('video-cover-preview'));
    $http.get(collectionUrl + 'is_member_of')
      .success(function(res){
        console.log(res);
      })
  }]);

});
