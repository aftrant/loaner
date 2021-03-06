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
import {MatTooltipModule} from '@angular/material';
import {BrowserModule} from '@angular/platform-browser';

import {DamagedModule} from '../../../../../shared/components/damaged';
import {ExtendModule} from '../../../../../shared/components/extend';
import {GuestModeModule} from '../../../../../shared/components/guest';
import {GreetingsCardModule} from '../../../../../shared/components/loan_management/greetings_card';
import {LoanActionsCardModule} from '../../../../../shared/components/loan_management/loan_actions_card';
import {LostModule} from '../../../../../shared/components/lost';
import {MaterialModule} from '../../core/material_module';
import {DeviceService} from '../../services/device';

import {DeviceInfoCard} from './device_info_card';

export * from './device_info_card';

@NgModule({
  declarations: [
    DeviceInfoCard,
  ],
  exports: [
    DeviceInfoCard,
  ],
  imports: [
    BrowserModule,
    DamagedModule,
    ExtendModule,
    FormsModule,
    GreetingsCardModule,
    GuestModeModule,
    LoanActionsCardModule,
    LostModule,
    MaterialModule,
    MatTooltipModule,
  ],
  providers: [
    DeviceService,
  ],
})
export class DeviceInfoCardModule {
}
