import psutil
import line_profiler
import os
from datetime import datetime

def profile(script_name):
    def decorator(func):
        profiler = line_profiler.LineProfiler()

        def wrapper(*args, **kwargs):
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_dir = '/reports'
            os.makedirs(report_dir, exist_ok=True)
            file_name = os.path.join(report_dir, f"{script_name}_{date_str}.txt")

            # Medir o uso de CPU antes da execução
            cpu_inicial = psutil.cpu_percent(interval=None)

            # Medir a memória antes da execução
            memoria_inicial = psutil.Process().memory_info().rss / (1024 * 1024)  # MB

            # Executar a função
            result = func(*args, **kwargs)

            # Medir a memória após a execução
            memoria_final = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
            memoria_usada = memoria_final - memoria_inicial  # Diferença

            profiler.add_function(func)
            profiler.enable()
            func(*args, **kwargs)
            profiler.disable()

            with open(file_name, "w") as f:
                f.write("Resultado da função: {}\n".format(result))
                f.write("Uso de CPU: {}%\n".format(cpu_inicial))
                f.write("Memória usada pela função: {:.2f} MB\n".format(memoria_usada))
                profiler.print_stats(stream=f)

            return result

        return wrapper
    return decorator
