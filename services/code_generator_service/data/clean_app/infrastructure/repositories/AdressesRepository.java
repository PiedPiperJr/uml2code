package org.enspy.4gi.infrastructure.repositories;

import org.enspy.4gi.domain.entities.Adresses;
import org.enspy.4gi.domain.repositories.IAdressesRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface AdressesJpaRepository extends JpaRepository< Adresses, UUID>, IAdressesRepository< Adresses, UUID>
{
    //TODO: Implement the repository logic here base on the AI
}