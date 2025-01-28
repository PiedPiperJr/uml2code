import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcessingProgressComponent } from './processing-progress.component';

describe('ProcessingProgressComponent', () => {
  let component: ProcessingProgressComponent;
  let fixture: ComponentFixture<ProcessingProgressComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProcessingProgressComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProcessingProgressComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
