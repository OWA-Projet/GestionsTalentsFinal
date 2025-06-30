import { Component } from '@angular/core';
import { User, UserService } from '../../core/user.service';
import { Router } from '@angular/router';
import { Observable, Subject, of } from 'rxjs';
import { switchMap, tap, catchError, shareReplay, startWith } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-list',
  templateUrl: './utilisateur-list.component.html',
  styleUrls: ['./utilisateur-list.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class UserListComponent {
  private refresh$ = new Subject<void>();
  users$!: Observable<User[]>;
  error: string | null = null;

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
    this.users$ = this.refresh$.pipe(
      startWith(void 0),
      switchMap(() =>
        this.userService.getAll().pipe(
          tap(() => this.error = null),
          catchError(() => {
            this.error = "Erreur lors du chargement des utilisateurs.";
            return of([] as User[]);
          })
        )
      ),
      shareReplay(1)
    );
  }

  ajouterUser() {
    this.router.navigate(['/user-formulaire']);
  }

  modifierUser(id: number) {
    this.router.navigate(['/user-formulaire', id]);
  }

  supprimerUser(id: number) {
    if (!confirm("Supprimer cet utilisateur ?")) return;
    this.userService.delete(id).subscribe({
      next: () => this.refresh$.next(),
      error: () => this.error = "Erreur lors de la suppression."
    });
  }
}
