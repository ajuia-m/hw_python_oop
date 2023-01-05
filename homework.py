M_IN_KM = 1000
LEN_STEP = 1.00

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, 
                 training: str,
                 duration: float, 
                 distance: float,
                 speed: float,
                 calories: float,) -> None:

        self.training_type = training
        self.duration = duration
        self.distance = distance
        self.speed = speed 
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type} ; ',
                f'Длительность: {self.duration.f3} ч.; ',
                f'Дистанция: {self.distance.f3} км; ',
                f'Потрачено ккал: {self.calories.f3}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * LEN_STEP / M_IN_KM)
        

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance(self.action)/self.duration)
        

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Traing type error messaging as parent
        return 'Ошибка: утерян тип тренировки'

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__name__,
                           self.duration,
                           self.get_distance, 
                           self.get_mean_speed,
                           self.get_spent_calories)
    

class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed(self.distance, self.duration)
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / M_IN_KM * self.duration)

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2 = 0.029

    def __init__(self, 
                 action: int,
                 duration: float, 
                 weight: float, 
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height #в метрах

    def get_spent_calories(self) -> float:
        return (((SportsWalking.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed(self.distance, self.duration)**2 / self.height)
                * SportsWalking.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight) * self.duration))
    

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_SPEED_MULTIPLIER = 1.1

    def __init__(self,
                 action: int, 
                 duration: float, 
                 weight: float, 
                 length_pool: float, 
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool  # длина бассейна в метрах.
        self.count_pool = count_pool    # сколько раз пользователь переплыл бассейн,
                                        # типом float учтено, что пользователь может сдаться на пол пути
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed + Swimming.CALORIES_SPEED_MULTIPLIER)
                * Swimming.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration)

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    print(data)
    return (training_types[workout_type](data))


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message)

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

