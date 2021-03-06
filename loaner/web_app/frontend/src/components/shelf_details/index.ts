// Copyright 2018 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {BrowserModule} from '@angular/platform-browser';
import {RouterModule} from '@angular/router';
import {ViewonlyLabelModule} from '../../components/viewonly_label';
import {MaterialModule} from '../../core/material_module';
import {Dialog, DialogsModule} from '../../services/dialog';
import {ShelfService} from '../../services/shelf';

import {ShelfDetails} from './shelf_details';

export * from './shelf_details';

@NgModule({
  declarations: [
    ShelfDetails,
  ],
  exports: [
    ShelfDetails,
  ],
  imports: [
    BrowserModule,
    DialogsModule,
    FormsModule,
    MaterialModule,
    RouterModule,
    ViewonlyLabelModule,
  ],
  providers: [
    ShelfService,
  ],
})
export class ShelfDetailsModule {
}
