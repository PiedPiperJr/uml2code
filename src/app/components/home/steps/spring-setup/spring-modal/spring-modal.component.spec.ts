import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpringModalComponent } from './spring-modal.component';

describe('SpringModalComponent', () => {
  let component: SpringModalComponent;
  let fixture: ComponentFixture<SpringModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpringModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpringModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
