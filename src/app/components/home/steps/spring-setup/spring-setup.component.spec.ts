import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpringSetupComponent } from './spring-setup.component';

describe('SpringSetupComponent', () => {
  let component: SpringSetupComponent;
  let fixture: ComponentFixture<SpringSetupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpringSetupComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpringSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
