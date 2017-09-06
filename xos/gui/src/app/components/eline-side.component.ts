
/*
 * Copyright 2017-present Open Networking Foundation

 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 * http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


let self;

class ElineSide {

  static $inject = ['XosSidePanel', 'XosModelStore', '$http', '$log', 'toastr', 'XosConfirm'];

  constructor(
    private XosSidePanel: any,
    private XosModelStore: any,
    private $http: any,
    private $log: any,
    private toastr: any,
    private XosConfirm: any,
  ) {
    self = this;
  }

  public saveEline(item: any) {
    let path = item.path;
    delete item.path;
    item.$save().then((res) => {
      item.path = path;
      this.toastr.success(`${item.name} successfully saved!`);
    })
      .catch((error) => {
        this.toastr.error(`Error while saving ${item.name}: ${error.specific_error}`);
      });
  }

  public deleteEline(item: any) {
    let name = item.name;
    this.XosConfirm.open({
      header: 'Confirm deletion',
      text: 'Are you sure you want to delete this? This action cannot be undone.',
      actions: [{
        label: 'Delete',
        class: 'btn-danger',
        cb: () => {
          item.$delete().then((res) => {
            this.toastr.success(`${name} successfully deleted!`);
          })
            .catch((error) => {
              this.toastr.error(`Error while deleting ${name}: ${error.specific_error}`);
            });
        }
      }]
    });

  }


}

export const elineSide: angular.IComponentOptions = {
  template: require('./eline-side.component.html'),
  controllerAs: 'vm',
  controller: ElineSide,
  bindings: {
    vng: '='
  }
};
