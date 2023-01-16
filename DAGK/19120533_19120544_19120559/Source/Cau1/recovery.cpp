#include <iostream>
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

/*  Một số hàm bổ trợ */
// Hàm này sẽ trích xuất ra 1 dãy byte con trong dãy cha, kết quả trả về là: arr[start, end)
char* extract(char* arr, int start, int byte_size){
    char* result = new char[byte_size];
    for (int i = start; i < start + byte_size; i++)
        result[i] = arr[i];

    return result;
}
/**/

/*
Đây là cấu trúc bootsector của FAT32, tổng các phần tử sẽ là 512 byte, ta sẽ đọc sector 0 vào
biến này để có thể biết được thông tin của bootsector
Ref: https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html
*/
struct FAT32 {
    uint8_t bootstrapJump[3];     // 	JumpCode ( 0 - 3 )
    uint8_t oem[8];               // 	OEM name/version (3 - 8)
    uint8_t bytePerSector[2];     // 	Byte per sector (B - 2)
    uint8_t sectorPerCluster;     // 	Sector per cluster (D - 1)
    uint8_t sectorInBootSector[2];    // 	Number of reserved sectors (E - 2)
    uint8_t fatCopy;              // 	Number of FAT copies (10 - 1)
    uint8_t rdetEntry[2];         // 	Number of root directory entries (11 - 2)
    uint8_t sector_of_Volume[2];  //     Total number of sector of Volume (13 - 2)
    uint8_t mediaType;            // 	Media descriptor type (15 - 1 )
    uint8_t sectorPerFAT[2];      // 	Sector per FAT, 0 for FAT32 ( 16 - 2 )
    uint8_t sectorPerTrack[2];    // 	Sector per track ( 18 - 2 )
    uint8_t head[2];              // 	Number of heads ( 1A - 2 )
    uint8_t hiddenSector[4];      // 	Number of hidden sectors ( 1C - 4 )
    uint8_t Total_sector[4];      //     Volume size ( 20 - 4 ) Sv
    uint8_t SectorperFAT[4];      //     Sector per FAT ( 24 - 4 ) Sf
    uint8_t Extended_flag[2];     //     (28-2)
    uint8_t Version[2];           //     Version of FAT32 (2A - 2)
    uint8_t Root_cluster[4];      //     Root Cluster (2C - 4)
    uint8_t System_inf_sector[2]; //     Empty cluster inf (30 - 2)
    uint8_t Backup_boot_sec[2];   //     Backup Boot Sector (32-2)
    uint8_t S6[12];               //     (34 - C )
    uint8_t Physical_drive;       //     Physical drive(40 - 1 )
    uint8_t Reversed;             //     (41 - 1)
    uint8_t Extended_signature;   //     (42 - 1)
    uint8_t Serial[4];            //     (43 - 4)
    uint8_t Volume_label[11];     //     (47 - B)
    uint8_t Fat_name[8];          //     (52 - 8)
    uint8_t BootrapCode[420];     //     (5A - 1A4)
    uint8_t signatrue[2];         //     (1FE - 2)
};

void FileRecover(string volume){
    // Đầu tiên ta sẽ đọc thông tin bootsector vào biến bootsector
    FAT32 bootsector = (char*)ReadSector(volume, 0, 1);
    
    // Tiếp theo ta sẽ tính vị trí bảng FAT và vị trí bảng RDET để thuận lợi cho việc khôi phục file.
    int fat_pos_1 = bootsector.sectorInBootSector;
    int fat_pos_2 = fat_pos_1 + bootsector.SectorperFAT;
    int rdet_pos = bootsector.sectorInBootSector + 2*bootsector.SectorperFAT;

    // Ta sẽ đọc lần lượt từng entry trong RDET và khôi phục nếu nó bị xóa.
    int index = 0;
    FAT32 entry;
    while (1){  
        (char*)entry = readBlock(volume, rdet_pos, index, 32);  // đọc entry của RDET vào biến entry.

        if (entry[0] == '0') // Nếu byte đầu là 0 thì ta dừng, nghĩa là đã hết file trong RDET
            break;
        if (entry[0] != 'E5')   // Nếu byte đầu khác E5 nghĩa là file vẫn bình thường
            continue;
        else    // nghĩa là byte đầu là E5 và  ta sẽ tiến hành khôi phục.
        {
            // Đầu tiên, Đổi tên file được khôi phục, kí tự đầu tiên file là f
            writeBlock(volume, rdet_pos, 0, 1, 'f');

            // Tiếp theo ta sẽ tìm vị trí cluster bắt đầu của file
            // Entry chiếm 32 byte, muốn biết cluster bắt đầu của file ta sẽ lấy
            // 2 byte tại vị trí 20 (byte cao) cộng 2 byte tại vị trí 26 (byte thấp)
            int cluster_start = extract(entry, 20, 2) + extract(entry, 26, 2);

            // Tiếp theo ta sẽ đi đến vị trí bảng FAT và thay đổi con trỏ cluster
            // Ta có: trong bảng FAT, mỗi phần tử chiếm 4 byte
            /*
                Phần này chưa hoàn thành
            */
        }
        
        index++;
    }

}

int main(){
    string path = "E:/";    // Path to your disk
    FileRecover(path);

    return 0;
}