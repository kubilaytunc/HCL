1. pardus-probe paketi yüklenmeden devices.json dosyası oluşmuyor. Depodaki pardus-probe paketini açıp bağımlılıklarını ve
değiştirdiği kısımları paket yaparken paket özelliklerine ekleyeceğiz.

2. Değişiklikler yeterli noktaya gelince paket haline getirip bir başlatıcı yazacağız.

3. Listeler güncellendiğinde UI ekranını yeniden yükleyerek değişiklikleri anlık görmeliyiz.



##Neredeyiz

1. libjson-xs-perl paketi hw-probe'a ek olarak kurulduğunda, istenilen devices.json dosyasını kendisi oluşturuyor. Böylece eski versiyon pardus-probe yüklemenin hiçbir gerekliliği kalmamış oluyor.

