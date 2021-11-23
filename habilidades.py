import shlex

class Habilidad:
    '''Abstracción del concepto de habilidad en un asistente.'''

    def __init__(self, nombre, descripcion=None):
        raise NotImplementedError

    def invocar(self):
        raise NotImplementedError

    def ayuda(self):
        raise NotImplementedError


class Divisas(Habilidad):
    '''Conversión de divisas'''
    def __init__(self, *args, tasa=0.85, **kwargs):
        raise NotImplementedError

    def invocar(self, cantidad):
        '''Convertir una cantidad la divisa original a la divisa objetivo'''
        raise NotImplementedError

class Menu:
    '''Menú interactivo de gestión de habilidades.'''

    def __init__(self, habilidades):
        # habilidades es una LISTA
        # self.habilidades es un diccionario de nombre -> habilidad
        self.habilidades = {}
        raise NotImplementedError

    def ayuda(self, comando=None):
        '''
        Muestra ayuda del uso del menú. Si no se especifica una habilidad,
        se muestra la ayuda general. Esta ayuda general muestra la lista
        de habilidades, una por línea, y la descripción de cada habilidad.

        Si se especifica una habilidad, se muestra su ayuda específica.
        '''
        if not comando:
            print('Habilidades disponibles:')
            for hab in self.habilidades.values():
                print(f'\t{hab.nombre}:\t{hab.descripcion}')
            return
        if comando not in self.habilidades:
            print(f'Habilidad no encontrada: {comando}')
            return
        self.habilidades[comando].ayuda()

    def lanzar(self):
        '''Recibe instrucciones del usuario en bucle.'''
        while True:
            linea = input('> ')
            if self.ejecutar(linea):
                break

    def convertir_linea(self, linea):
        comando, *args = shlex.split(linea)
        return comando, args

    def ejecutar(self, linea):
        '''
        Recibe una línea del usuario y ejecuta la acción requerida

        Devuelve True cuando se desea parar la ejecución.
        '''
        comando, args = self.convertir_linea(linea)
        raise NotImplementedError

    def emular(self, linea):
        '''Ejecuta una línea, mostrando por pantalla el comando'''
        print('>', linea)
        self.ejecutar(linea)

class MenuComas(Menu):
    pass

class MenuPrompt(Menu):
    pass

class MenuPreguntas(Menu):
    pass

def prueba_menu_simple():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38, descripcion='Conversión de bitcoins a euros'),
        Divisas('euro2bitcoin', tasa=1/49929.38, descripcion='Conversión de euros a bitcoins'),
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('bitcoin2euro 100')
    m.emular('euro2bitcoin 100')
    m.emular('ayuda noexiste')
    m.emular('ayuda bitcoin2euro')

class HabilidadCompleja(Habilidad):
    '''Un tipo de habilidad que permite invocar varios sub-comandos'''

    def subcomandos(self):
        '''
        Devuelve un diccionario de subcomandos a funciones.
        
        p.e.:
            {
            'insertar': self.insertar_producto,
            'borrar': self.borrar_producto,
            }
        '''
        return {}

    def invocar(self, subcomando, *args):
        raise NotImplementedError

    def ayuda(self):
        print('Comando:\t', self.nombre)
        print('Descripción:\t', self.descripcion)
        print('Subcomandos:')
        # Muestra información de cada uno de los subcomandos
        raise NotImplementedError


class ListaDeLaCompra(HabilidadCompleja):
  '''Gestión muy simple de lista de la compra'''

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.productos = []

  def subcomandos(self):
    return {
      'insertar': self.insertar,
      'borrar': self.borrar,
      'listar': self.listar,
      'cantidad': self.cantidad,
      }

  def insertar(self, producto):
    '''Insertar un producto nuevo'''
    self.productos.append(producto)

  def listar(self):
    '''Mostrar el listado de productos'''
    for ix, producto in enumerate(self.productos):
      print(f'{ix}: {producto}')

  def borrar(self, numero):
    '''Borrar un producto'''
    self.productos.pop(int(numero))

  def cantidad(self):
    '''Mostrar el número de productos en la lista'''
    return len(self.productos)

def prueba_menu_complejas():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaDeLaCompra('listadelacompra', 'Gestión de la lista de la compra')
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('ayuda listadelacompra')
    m.emular('listadelacompra insertar "1 kg de plátanos canarios"')
    m.emular('listadelacompra insertar "Pimientos"')
    m.emular('listadelacompra listar')
    m.emular('listadelacompra borrar 0')
    m.emular('listadelacompra listar')

if __name__ == '__main__':
    print('#' * 10, 'Prueba menú simple')
    prueba_menu_simple()
    print('#' * 10, 'Prueba menú complejas')
    prueba_menu_complejas()
