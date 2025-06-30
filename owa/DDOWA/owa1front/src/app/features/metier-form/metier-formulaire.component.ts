import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MetierService, Metier } from '../../core/metier.service';
import { BehaviorSubject } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-metier-formulaire',
  templateUrl: './metier-formulaire.component.html',
  styleUrls: ['./metier-formulaire.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class MetierFormulaireComponent implements OnInit {
  form: FormGroup;
  isEdit = false;
  metierId: number | null = null;
  error: string | null = null;
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private metierService: MetierService
  ) {
    this.form = this.fb.group({
      nom: ['', Validators.required],
      description: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.isEdit = true;
        this.metierId = +id;
        this.loadingSubject.next(true);
        this.metierService.get(this.metierId).subscribe({
          next: (metier: Metier) => {
            this.form.patchValue(metier);
            this.loadingSubject.next(false);
          },
          error: () => {
            this.error = "Erreur lors du chargement du métier.";
            this.loadingSubject.next(false);
          }
        });
      }
    });
  }

  onSubmit() {
    if (this.form.invalid) return;
    this.loadingSubject.next(true);
    this.error = null;
    const values = this.form.value;
    let obs$;
    if (this.isEdit && this.metierId) {
      obs$ = this.metierService.update(this.metierId, values);
    } else {
      obs$ = this.metierService.create(values);
    }
    obs$.subscribe({
      next: () => {
        this.loadingSubject.next(false);
        this.router.navigate(['/metier-list']);
      },
      error: () => {
        this.error = "Erreur lors de la " + (this.isEdit ? "modification." : "création.");
        this.loadingSubject.next(false);
      }
    });
  }
}
