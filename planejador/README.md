# Personal Financial Planner (Streamlit)

A web application developed with Python + Streamlit to support personal financial planning, allowing simulations with pessimistic, realistic, and optimistic scenarios, considering fixed and variable income and expenses.

The system provides:

* Monthly financial reserve projections
* Scenario comparison
* Interactive charts
* Export a PDF report with a summary of results

---

## Features

* Monthly financial data input
* Support for single values or ranges for variable income and expenses

  * Example: `600 to 1000` or `250 - 400`
* Automatic simulation of three scenarios:
  * Pessimistic
  * Realistic
  * ptimistic

* Single comparative chart for all scenarios
* PDF report export
* Use of `session_state` for data persistence within the app

---

## Scenario Logic

| Scenario    | Variable Income | Variable Expenses |
| ----------- | --------------- | ----------------- |
| Pessimistic | Minimum value   | Maximum value     |
| Realistic   | Average value   | Average value     |
| Optimistic  | Maximum value   | Minimum value     |

---

## Technologies Used

* **Python 3**
* **Streamlit**
* **Pandas**
* **ReportLab** (PDF generation)

---

## Project Structure

```
financial-planner/
│
├── app.py              # Streamlit interface
├── financeiro.py       # Financial planning logic
├── requirements.txt    # Project dependencies
└── README.md
```

---

##  Running Locally

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/financial-planner-streamlit.git
```

2. Navigate to the project folder:

```bash
cd financial-planner-streamlit
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

---

## Deployment

The app is designed to work seamlessly on **Streamlit Community Cloud**, with automatic deployment directly from GitHub.

---

## PDF Export

The PDF report includes:

* Financial goal
* Scenario comparison
* Months required to reach the goal
* Final reserve in each scenario
* Scenario comparison chart

---

## Educational Context

This project can also be used as:

* A teaching tool in technology-related classes
* A practical example of financial modeling with programming
* A basis for studies on **digital literacy and decision-making**

---

## Author

**Marcus Vinícius de Freitas da Silva**
Teacher • Developer • Researcher in Education and Technology

---

## Future Improvements

* User authentication
* Simulations with additional contributions
* Inflation adjustment
* More advanced dashboard
* Mobile-first version

---

💡 *Feel free to clone, study, adapt, and extend this project.*
