#include <iostream>
using namespace std;

/*
        Đây là cấu trúc của BootSector và entry của RDET trong bản tự thiết kế trong câu 2
*/

struct BootSector {
    uint8_t volume_name[8];         // name of volume
    uint8_t bytePerSector[2];     // 	Byte per sector (B - 2)
    uint8_t sectorPerCluster;     // 	Sector per cluster (D - 1)
    uint8_t countFat;              // 	Number of FAT table (10 - 1)
    uint8_t Total_sector[4];      //     Volume size ( 20 - 4 ) Sv
    uint8_t SectorperFAT[4];      //     Sector per FAT ( 24 - 4 )
    uint8_t Root_cluster[4];      //     start Cluster of RDET(2C - 4)
    uint8_t empty_cluster[4];     // number of empty cluster
    uint8_t copy_of_bootsector[2];  // sector contains copy of bootsector
    uint8_t password[32];          // password of volume
    uint8_t sector_of_boot[2];      // number of sector's bootsector
    uint8_t reserved[448];         // reserved byte to further development
};

struct RDET_entry{
    uint8_t file_name[8];      // name of file
    uint8_t extension[3];      // extension of file
    uint8_t status[1];         // status attribute of file
    uint8_t password[8];        // password of file
    uint8_t cluster_start[4];   // cluster start of file
    uint8_t hour_updated[2];    // giờ cập nhập của file
    uint8_t day_updated[2];     // ngày cập nhập của file
    uint8_t size[4];            // size of file
};