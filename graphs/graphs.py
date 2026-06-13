import matplotlib.pyplot as plt

scores = [0, 1, 2, 3, 4]
counts = [600, 600, 600, 600, 600]  # perfectly balanced

plt.bar(scores, counts)
plt.xlabel("Sensationalism Score")
plt.ylabel("Number of Headlines")
plt.title("Dataset Distribution Across Sensationalism Levels")
plt.xticks(scores)
plt.show()

models = ["TF-IDF + KNN", "CNN-LSTM", "Transformer", "SensaScore"]
accuracy = [78, 74, 83, 85]

plt.bar(models, accuracy)
plt.ylabel("Accuracy (%)")
plt.title("Model Performance Comparison")
plt.xticks(rotation=20)
plt.show()

labels = ["0", "1", "2", "3", "4"]
sizes = [20, 20, 20, 20, 20]

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title("Score Distribution")
plt.show()

metrics = ["MAE", "MSE", "R2 Score"]
values = [0.45, 0.35, 0.82]

plt.bar(metrics, values)
plt.title("Regression Performance Metrics")
plt.show()

metrics = ["MAE", "MSE", "R2 Score"]
values = [0.45, 0.35, 0.82]

plt.bar(metrics, values)
plt.title("Regression Performance Metrics")
plt.show()