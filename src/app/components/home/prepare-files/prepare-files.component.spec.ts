import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrepareFilesComponent } from './prepare-files.component';

describe('PrepareFilesComponent', () => {
  let component: PrepareFilesComponent;
  let fixture: ComponentFixture<PrepareFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrepareFilesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrepareFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
