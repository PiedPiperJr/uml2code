import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloadFilesComponent } from './download-files.component';

describe('DownloadFilesComponent', () => {
  let component: DownloadFilesComponent;
  let fixture: ComponentFixture<DownloadFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DownloadFilesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DownloadFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
