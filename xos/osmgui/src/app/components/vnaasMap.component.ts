
/*
 * Copyright 2017-present Open Networking Foundation

 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 * http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


import {NgMap} from 'ngmap';
import {Subscription} from 'rxjs/Subscription';
import * as _ from 'lodash';
import * as L from 'leaflet';

declare var google;

let self;

export class VnaasMap {

  static $inject = [
    'XosModelStore',
    'AppConfig',
    '$resource',
    'XosSidePanel',
    'XosModelDiscoverer',
    'ModelRest',
    'MapConfig',
    'leafletData',
    'leafletMarkerEvents',
    '$scope'
  ];

  public unis = [];
  public elines = [];
  public cpilatlng = new Map();
  public paths = {};
  public bwps = [];
  public map;
  public panelOpen = false;
  public createMode = false;
  public canCreateEline = true;
  public eline;
  public current_uni;
  public mapDefaults = {minZoom: 2, attributionControl: false};
  public markers = {};
  public events = {};

  private uniSubscription: Subscription;
  private elineSubscription: Subscription;
  private bwpSubscription: Subscription;

  constructor(
    private XosModelStore: any,
    private AppConfig: any,
    private $resource: any,
    private XosSidePanel: any,
    private XosModelDiscoverer: any,
    private ModelRest: any,
    private MapConfig: any,
    private leafletData: any,
    private leafletMarkerEvents: any,
    private $scope: any
  ) {
    self = this;
  }

  $onInit() {

    this.leafletData.getMap('vnaasMap').then(map => {
      this.map = map;
      this.uniSubscription = this.XosModelStore.query('UserNetworkInterface', '/vnaas/usernetworkinterfaces/').subscribe(
        res => {
          this.unis = res;
          this.renderMap(map);
        }
      );
      this.elineSubscription = this.XosModelStore.query('ELine', '/vnaas/elines/').subscribe(
        res => {
          this.elines = res;
          this.createPaths();
          this.renderMap(map);
        }
      );
      this.bwpSubscription = this.XosModelStore.query('BandwidthProfile', '/vnaas/bandwidthprofiles/').subscribe(
        res => {
          this.bwps = res;
        }
      );
    });
  }

  $onDestroy() {
    if (this.uniSubscription) {
      this.uniSubscription.unsubscribe();
    }
    if (this.elineSubscription) {
      this.elineSubscription.unsubscribe();
    }
    if (this.bwpSubscription) {
      this.bwpSubscription.unsubscribe();
    }
  }

  public renderMap(map: any) {
    let bounds = L.latLngBounds([]);

    let markerScope = this.$scope.$new();
    markerScope.vm = this;

    for (let i = 0; i < self.unis.length; i++) {

      self.unis[i].eline_start = false;

      let curr = JSON.parse(self.unis[i].latlng);
      this.cpilatlng.set(self.unis[i].cpe_id, curr);
      let coords = L.latLng(curr);
      bounds.extend(coords);

      this.markers[`marker${self.unis[i].id}`] = {
        lat: coords.lat,
        lng: coords.lng,
        draggable: false,
        icon: {
          iconUrl: this.MapConfig.marker,
          iconSize: [30, 32],
          iconAnchor: [15, 32],
          popupAnchor: [0, -32]
        },
        message: this.popupHTML(self.unis[i]),
        getMessageScope: () => markerScope
      }
    }

    map.fitBounds(bounds);

  }

  public popupHTML(uni: any) : String {
    return `
        <div class="marker-info">
            <h4>${uni.name}</h4>
            <p>
                <b>LatLng: </b>${uni.latlng.toString()}<br/>
                <b>Cpe id: </b>${uni.cpe_id}<br/>
                <b>Tenant: </b>${uni.tenant}<br/>
            </p>
            <button ng-show="vm.canCreateEline" ng-click="vm.createConnection(${uni.id})()">Create connection</button>
            <button ng-show="!vm.canCreateEline && !uni.eline_start" ng-click="vm.finishConnection(${uni.id})">Finish connection</button>
        </div>`;
  }

  public createPaths() {
    this.elines.forEach((eline: any) => {
      let latlng_start = this.cpilatlng.get(eline.connect_point_1_id);
      let latlng_end = this.cpilatlng.get(eline.connect_point_2_id);
      this.paths[`eline${eline.id}`] = {
        type: 'polyline',
        latlngs: [{lat: latlng_start[0], lng: latlng_start[1]}, {lat: latlng_end[0], lng: latlng_end[1]}],
        color: this.colorLine(eline.backend_status),
        weight: 5
      }
    });

  }

  public colorLine(eline_status : any) {
    let status = parseInt(eline_status, 10);
    switch (status) {
      case 0:
        return '#f39c12';
      case 1:
        return '#2ecc71';
      default:
        return '#e74c3c';
    }
  }

  public elinePanel(e: any, eline: any, exists: boolean) {

    self.panelOpen = !self.panelOpen;
    if (exists) {
      self.eline = _.find(self.elines, {id: eline.id});
    }
    self.XosSidePanel.toggleComponent('elineSide', {vng: self}, false);
    if (!self.panelOpen && self.createMode) {
      self.createMode = false;
      self.canCreateEline = true;
      self.current_uni.eline_start = false;
    }

  }

  public createConnection(uniId: any) {
    return () => {
      let uni = _.find(this.unis, {id: uniId});
      self.canCreateEline = false;
      self.createMode = true;
      uni.eline_start = true;
      self.current_uni = uni;
      self.eline = {
        name: uni.name,
        uni1name: uni.name,
        connect_point_1_id: uni.cpe_id,
      };
      self.elinePanel({}, self.eline, false);
    };

  }

  public finishConnection(uniId: any) {
    let uni = _.find(self.unis, {id: uniId})
    self.eline.connect_point_2_id = uni.cpe_id;
    if (self.eline.name === self.eline.uni1name) {
      self.eline.name = self.eline.name + uni.name;
    }
    delete self.eline.uni1name;
    const resource = this.ModelRest.getResource('/vnaas/elines/');
    let res = new resource({});
    for (let attr in self.eline) {
      if (true) {
        res[attr] = self.eline[attr];
      }

    }
    self.eline = res;
  }

}

export const vnaasMap: angular.IComponentOptions = {
  template: require('./vnaasMap.component.html'),
  controllerAs: 'vm',
  controller: VnaasMap,
};
