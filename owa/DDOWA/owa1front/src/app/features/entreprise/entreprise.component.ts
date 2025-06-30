import { Component } from '@angular/core';
import { Entreprise, EntrepriseService } from '../../core/entreprise.service';
import { Router } from '@angular/router';
import { Observable, Subject, of } from 'rxjs';
import { switchMap, tap, catchError, shareReplay, startWith } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-entreprise-list',
  templateUrl: './entreprise.component.html',
  styleUrls: ['./entreprise.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class EntrepriseListComponent {
  private refresh$ = new Subject<void>();
  entreprises$!: Observable<Entreprise[]>;
  error: string | null = null;

  constructor(
    private entrepriseService: EntrepriseService,
    private router: Router
  ) {}

  ngOnInit() {
    this.entreprises$ = this.refresh$.pipe(
      startWith(void 0),
      switchMap(() =>
        this.entrepriseService.getAll().pipe(
          tap(() => this.error = null),
          catchError(() => {
            this.error = "Erreur lors du chargement des entreprises.";
            return of([] as Entreprise[]);
          })
        )
      ),
      shareReplay(1)
    );
  }

  ajouterEntreprise() {
    this.router.navigate(['/entreprise-formulaire']);
  }

  modifierEntreprise(id: number) {
    this.router.navigate(['/entreprise-formulaire', id]);
  }

  supprimerEntreprise(id: number) {
    if (!confirm("Supprimer cette entreprise ?")) return;
    this.entrepriseService.delete(id).subscribe({
      next: () => this.refresh$.next(),
      error: () => this.error = "Erreur lors de la suppression."
    });
  }
}
