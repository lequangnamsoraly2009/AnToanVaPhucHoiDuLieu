#include "data.h"
#include <fstream>
using namespace std;

/*      
        Có một vài hàm cần thiết nhưng em không viết được nên em sẽ giả sử là đã tổn tại hàm đó và sẽ lấy để dùng. 
        Notes: Đây chỉ là đoạn code mang tính tương đối, nếu chạy thì sẽ báo lỗi.
*/

/*
Giả sử ta đã có 2 hàm ReadSector và WriteSector.
Cách dùng: đọc một lượng num sector từ vị trí 1 sector nào đó.
- Tham số:
    volume: là chuỗi tên của volume cần thao tác
    sector: vị trí của sector muốn đọc/ghi vào
    num: số lượng sector cần đọc/ghi vào tính từ vị trí sector ở trên (đơn vị: sector).
    - Đối với WriteSector có tham số value là giá trị cần ghi vào. Và hàm này trả về bool, nếu 1 là thành công.
*/
char* ReadSector(string volume, int sector, int num){}
bool WriteSector(string volume, int sector, int num, char* value){}
/*
Giả sử ta đã có 2 hàm ReadBlock và WriteBlock.
Cách dùng: hàm này sẽ đến vị trí sector cho trước, và đọc một lượng num_byte (byte) từ vị trí pos trong sector đó.
- Tham số:
    volume: là chuỗi tên của volume cần thao tác
    sector: vị trí của sector muốn đọc/ghi vào
    pos: vị trí byte thứ bao nhiêu trong sector đó
    num_byte: số lượng byte cần đọc/ghi tính từ vị trí pos trong sector đó (đơn vị: byte)
    - Đối với WriteBlock có tham số value là giá trị cần ghi vào. Và hàm này trả về bool, nếu 1 là thành công.
*/
char* readBlock(string volume, int sector, int pos, int num_byte){}
bool writeBlock(string volume, int sector, int pos, int num_byte, char* value){}



/*
    CÁC HÀM CHỨC NĂNG THEO YÊU CẦU CỦA ĐỀ BÀI
*/
void Lietkedanhsachfile(string volume){
    BootSector bootsector;

    // Đầu tiên, ta sẽ đọc nội dung bootsector vào biến bootsector.
    (char*)bootsector = ReadSector(volume, 0, 1);
    // Tiếp theo ta sẽ tính vị trí bảng RDET = số sector Bootsector + 2 x kích thước bảng FAT
    int rdet_pos = bootsector.sector_of_boot + 2*bootsector.SectorperFAT;
    
    // Ta sẽ sẽ đọc lần lượt từng entry như sau:
    int index = 0;
    RDET_entry entry;

    cout << "Danh sach file: " << endl;
    while (1){  // Ta sẽ đọc từng entry trong bảng RDET đến khi gặp byte đầu tiên là 0 thì dừng, nghĩa là đã hết
        (char*)entry = readBlock(volume, rdet_pos, index, 32);  // đọc entry trong RDET gán vào biến entry

        if (entry[0] == 'E5')   // Nếu byte đầu là E5 thì ta sẽ bỏ qua vì nó đã bị xóa
            continue;
        if (entry[0] == '0') // Nếu byte đầu là 0 thì ta dừng,
            break;
        
        // Nếu tới được đây thì file tồn tại và ta sẽ xuất file đó ra màn hình
        cout << entry.file_name << entry.extension << endl;

        index++;
    }
}

void createVolume(int size){
    ofstream volume("MyFS.dat", ios::binary | ios::out);

    int temp_data = 0;
    for (int i = 0; i < size*1000000; i++){
        volume.write((char*)temp_data, 4);
    }
    volume.close();
}

int main(){

    createVolume(100);
    Lietkedanhsachfile("MyFS.dat");
    
    return 0;
}