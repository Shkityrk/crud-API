package main

import (
	docs "crud/docs"
	"crud/src/infrastructure"
	"crud/src/interfaces/api"
	"crud/src/interfaces/database"
	"crud/src/usecase"
	"fmt"
	"log"
	"net/http"
	"os"

	httpSwagger "github.com/swaggo/http-swagger"
)

// @title CRUD API для пользователей
// @version 1.0
// @description REST API с использованием чистой архитектуры и MongoDB
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.email support@example.com

// @license.name MIT
// @license.url https://opensource.org/licenses/MIT

// @host localhost:8080
// @BasePath /
// @schemes http
func main() {
	// Настраиваем Swagger под HTTPS через nginx
	docs.SwaggerInfo.Schemes = []string{"https"}
	docs.SwaggerInfo.Host = "localhost"

	mongoURI := os.Getenv("MONGODB_URI")
	if mongoURI == "" {
		mongoURI = "mongodb://crud_mongodb:27017"
	}

	db, err := infrastructure.NewMongoDBConnection(mongoURI)
	if err != nil {
		log.Fatal("Failed to connect to MongoDB:", err)
	}

	userRepo := database.NewUserRepository(db)

	userInteractor := &usecase.UserInteractor{
		UserRepository: userRepo,
	}

	userController := &api.UserController{
		Interactor: userInteractor,
	}

	router := infrastructure.NewRouter()

	router.POST("/users", userController.Create)
	router.GET("/users", userController.GetAll)
	router.GET("/users/:id", userController.GetByID)
	router.PUT("/users/:id", userController.Update)
	router.DELETE("/users/:id", userController.Delete)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Объединяем handlers
	mux := http.NewServeMux()
	mux.Handle("/swagger/", httpSwagger.WrapHandler)
	mux.Handle("/", router)

	fmt.Printf("Server is running on port %s\n", port)
	fmt.Printf("Swagger UI: http://localhost:%s/swagger/index.html\n", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}
