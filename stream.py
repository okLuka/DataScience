import streamlit as st
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file):
    data = pd.read_csv(file)
    return data


def check_hypotheses(data, age_threshold, work_days_threshold):
    male_data = data[data['Пол'] == 'М']
    female_data = data[data['Пол'] == 'Ж']

    t_statistic_gender, p_value_gender = stats.ttest_ind(male_data['Количество больничных дней'], female_data['Количество больничных дней'])

    older_than_age_data = data[data['Возраст'] > age_threshold]
    younger_than_or_age_data = data[data['Возраст'] <= age_threshold]

    t_statistic_age, p_value_age = stats.ttest_ind(older_than_age_data['Количество больничных дней'], younger_than_or_age_data['Количество больничных дней'])

    return p_value_gender < 0.05, p_value_age < 0.05

def main():
    st.title("Проверка гипотез по данным")

    # Загрузка файла
    file = st.file_uploader("Загрузите CSV файл", type=['csv'])

    if file is not None:
        data = load_data(file)

        st.subheader("Исходные данные")
        st.write(data)

        age_threshold = st.slider("Пороговый возраст", min_value=int(data['Возраст'].min()), max_value=int(data['Возраст'].max()), value=int(data['Возраст'].mean()))
        work_days_threshold = st.slider("Пороговое количество рабочих дней", min_value=int(data['Количество больничных дней'].min()), max_value=int(data['Количество больничных дней'].max()), value=int(data['Количество больничных дней'].mean()))

        p_value_gender, p_value_age = check_hypotheses(data, age_threshold, work_days_threshold)
        st.subheader("Результаты проверки гипотез")
        st.write("Гипотеза 1: Мужчины пропускают в течение года более", work_days_threshold, "рабочих дней по болезни значимо чаще женщин")
        st.write("Результат:", "Статистически значимо" if p_value_gender else "Не статистически значимо")

        st.write("Гипотеза 2: Работники старше", age_threshold, "лет пропускают в течение года более", work_days_threshold, "рабочих дней по болезни значимо чаще своих более молодых коллег")
        st.write("Результат:", "Статистически значимо" if p_value_age else "Не статистически значимо")

        # Графики распределений
        st.subheader("Графики распределений")
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        sns.histplot(data=data, x='Количество больничных дней', hue='Пол', ax=axes[0])
        sns.histplot(data=data, x='Количество больничных дней', hue=data['Возраст'] > age_threshold, ax=axes[1])
        axes[0].set_title('Распределение по полу')
        axes[1].set_title('Распределение по возрасту')
        st.pyplot(fig)

if __name__ == "__main__":
    main()
