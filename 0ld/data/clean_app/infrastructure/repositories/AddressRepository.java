package org.enspy.4gi.infrastructure.repositories;

import org.enspy.4gi.domain.entities.Address;
import org.enspy.4gi.domain.repositories.IAddressRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface AddressJpaRepository extends JpaRepository< Address, UUID>, IAddressRepository< Address, UUID>
{
    //TODO: Implement the repository logic here base on the AI
}