import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TargetClassifierComponent } from './target-classifier.component';

describe('TargetClassifierComponent', () => {
  let component: TargetClassifierComponent;
  let fixture: ComponentFixture<TargetClassifierComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TargetClassifierComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TargetClassifierComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
