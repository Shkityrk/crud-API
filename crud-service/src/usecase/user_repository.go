package usecase

import "crud/src/domain"

type UserRepository interface {
	Create(user *domain.User) error
    GetByID(id int64) (*domain.User, error)
	GetAll() ([]*domain.User, error)
	Update(user *domain.User) error
    Delete(id int64) error
}
