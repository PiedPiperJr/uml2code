import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrepareFileComponent } from './prepare-file.component';

describe('PrepareFileComponent', () => {
  let component: PrepareFileComponent;
  let fixture: ComponentFixture<PrepareFileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrepareFileComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrepareFileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
